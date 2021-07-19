
import './App.css';
import React from 'react';
import Button from '@material-ui/core/Button';
import * as datav from '@jiaminghi/data-view-react'
import * as fund from './apis/fund'
import StickyHeadTable from './components/table'

function printData(){
  fund.fetchData("001182").then((res)=>{
    console.log(res)
  }).catch((err)=>{
    console.log("error:")
    console.log(err)
  })
}


function App() {
  const tableRef = React.createRef();
  return (
    <datav.FullScreenContainer>
      <datav.BorderBox4>
        <div className="main-content">
        <Button onClick={()=>{printData("001182")}}> 获取数据 </Button>
        <StickyHeadTable 
        
        
        /> 
        </div>
      </datav.BorderBox4>
    </datav.FullScreenContainer>
  );
}

export default App;
