import React from 'react'
import MedicalTerm from './medical-term'
import TextRecognition from './text-recognition'
import TextRecognitionCamera from './text-camera'
import SingleMedicalTerm from './singlemedical-term'

const Page = () => {
  return (
    <div>
      {/* <MedicalTerm/> */}
      <SingleMedicalTerm/>
      {/* <TextRecognition/> */}
      {/* <TextRecognitionCamera /> */}
    </div>
  )
}

export default Page; 