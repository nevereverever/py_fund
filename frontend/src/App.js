
import './App.css';
import React from 'react';
import {Button} from 'antd'
import * as datav from '@jiaminghi/data-view-react'
import * as fund from './apis/fund'
import {FundTable} from './components/table'


// async function printData(){
//   var numbers=[
//     "001182",
//     "161725",
//     "217017",
//     "011190",
//     "001986",
//     "001102",
//     "005609",
//     "007345",
//     "007340",
//     "163406",
//     "502056",
//     "001595",
//     "001594",
//     "011103",
//     "004683",
//     "167601",
//     "180012",
//     "007802",
//     "163409"
//   ]
//   for(var i=0;i<numbers.length;i++){
//     console.log(numbers[i])
//     await fund.fetchData(numbers[i]).then((res)=>{
//       console.log(res)
//     }).catch((err)=>{
//       console.log("error:")
//       console.log(err)
//     })
//   }
// }

const numbers=[
  "001182",
  "161725",
  "217017",
  "011190",
  "001986",
  "001102",
  "005609",
  "007345",
  "007340",
  "163406",
  "502056",
  "001595",
  "001594",
  "011103",
  "004683",
  "167601",
  "180012",
  "007802",
  "163409"
]

function App() {

  return (
    <datav.FullScreenContainer>
      <datav.BorderBox8>
        <div className="main-content">
        <FundTable numbers={numbers}> </FundTable>
        </div>
      </datav.BorderBox8>
    </datav.FullScreenContainer>
  );
}

export default App;
