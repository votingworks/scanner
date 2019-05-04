const fs = require("fs")
const path = require("path")
const { Image : ImageJS } = require('image-js')
const jsQR = require("jsqr")

import { BallotStyle , Contest , Contests , Ballot , CandidateContest } from './types'

// load all files from a directory
const input_path = path.join(__dirname, '..', 'ballots', 'tests')
const dir = fs.readdirSync(input_path)

// load the election
const election_path = path.join(__dirname, '..', 'electionSample.json')
const election = JSON.parse(fs.readFileSync(election_path))

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

dir.forEach((f : string) => {
  const file = path.join(input_path, f)
  // @ts-ignore image type not defined
  ImageJS.load(file).then(function(im) {
    const scanResult = scan(im)
    
    const qrData : string = scanResult.data as string

    const [ballotStyleId, precinctId, allChoices] = qrData.split(".")
    console.log(allChoices)
    // figure out the contests
    const ballotStyle = election.ballotStyles.find((b : BallotStyle)=> b.id === ballotStyleId)
    const contests : Contests = election.contests.filter((c : Contest) => ballotStyle.districts.includes(c.districtId))

    // prepare the CVR
    let votes : Ballot = {precinctId}

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

    console.log(precinctId, votes)

    // put CVR back together from QR code
    
    // output the CVR

  })
})

