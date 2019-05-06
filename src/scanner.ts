const fs = require("fs")
const path = require("path")
const { Image : ImageJS } = require('image-js')
const jsQR = require("jsqr")

import { BallotStyle , Contest , Contests , Ballot , CandidateContest } from './types'

// Command-Line Arguments:
const [electionPath, ballotDirectoryPath, cvrFilePath] = process.argv.slice(2).map(s => path.join(__dirname, '..', s))

// load all files from a directory
const dir = fs.readdirSync(ballotDirectoryPath)

// load the election
const election = JSON.parse(fs.readFileSync(electionPath))

// @ts-ignore image type not defined
const scan = (im) => {
  // look at rough regions where the QR code is expected
  
  const [width, height] = im.sizes

  const firstImage = im.crop({x: width*3/5, width: width/5, y:0, height: height/4})
  const firstScan = jsQR(firstImage.data, firstImage.width, firstImage.height)

  if (firstScan) {
    return firstScan
  }
  
  const secondImage = im.crop({x: width/5, width: width/5, y:height*3/4, height: height/4})
  const secondScan = jsQR(secondImage.data, secondImage.width, secondImage.height)
  return secondScan
}


var cvrStream = fs.createWriteStream(cvrFilePath);
cvrStream.once('open', () => {
  dir.forEach((f : string) => {
    const file = path.join(ballotDirectoryPath, f)

    // @ts-ignore image type not defined
    ImageJS.load(file).then(function(im) {
      const qrData : string = scan(im).data as string
      const [ballotStyleId, precinctId, allChoices] = qrData.split(".")

      // figure out the contests
      const ballotStyle = election.ballotStyles.find((b : BallotStyle)=> b.id === ballotStyleId)
      const contests : Contests = election.contests.filter((c : Contest) =>
	(ballotStyle.districts.includes(c.districtId) &&
	 (!ballotStyle.partyId ||
	  !c.partyId ||
	  ballotStyle.partyId === c.partyId)
	))


      // prepare the CVR
      let votes : Ballot = {}

      const allChoicesList = allChoices.split("/")
      contests.forEach((c : Contest, contest_num : number) => {
	if (c.type === "yesno") {
	  
	}
	
	if (c.type === "candidate") {
	  // choices for this question
	  const choices = allChoicesList[contest_num].split(",")
	  if (choices.length > 1 || choices[0] !== '') {
	    votes[c.id] = choices.map(choice => (c as CandidateContest).candidates[parseInt(choice)].id)
	  }
	}
      })
      
      cvrStream.write(`${precinctId}, ${JSON.stringify(votes)}\n`)
    })
  })
})
  
