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

dir.forEach((f : string) => {
  const file = path.join(input_path, f)
  // @ts-ignore image type not defined
  ImageJS.load(file).then(function(im) {
    const qrData : string = jsQR(im.data, im.width, im.height).data as string

    const [ballotStyleId, precinctId, choices] = qrData.split(".")
    console.log(choices)
    // figure out the contests
    const ballotStyle = election.ballotStyles.find((b : BallotStyle)=> b.id === ballotStyleId)
    const contests : Contests = election.contests.filter((c : Contest) => ballotStyle.districts.includes(c.districtId))

    // prepare the CVR
    let votes : Ballot = {precinctId}

    const choices_list = choices.split("/")
    contests.forEach((c : Contest, c_num : number) => {
      if (c.type === "yesno") {

      }

      if (c.type === "candidate") {
	const choice = choices_list[c_num]
	console.log(c.id, (c as CandidateContest).candidates.length)
	if (choice !== '') {
	  console.log("CHOICE", choice, c_num)
	  votes[c.id] = (c as CandidateContest).candidates[parseInt(choice)].id
	}
      }
    })

    console.log(precinctId, votes)

    
    // put CVR back together from QR code
    
    // output the CVR

  })
})

