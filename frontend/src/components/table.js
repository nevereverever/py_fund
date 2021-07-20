import {React,Component} from 'react';
import { Table, Button } from 'antd'
import * as fund from '../apis/fund'

// dwjz: "2.4440"
// fundcode: "001182"
// gsz: "2.4469"
// gszzl: "0.12"
// gztime: "2021-07-20 15:00"
// jzrq: "2021-07-19"
// name: "易方达安心回馈混合"
const columns = [
  {
    title: '姓名',
    dataIndex: 'name',
    sorter: true,
    width: '20%'
  },
  {
    title: '截止日期',
    dataIndex: 'jzrq',
  },
  {
    title: 'dwjz',
    dataIndex: 'dwjz',
  },
  {
    title: 'fundcode',
    dataIndex: 'fundcode',
  },
  {
    title: 'gsz',
    dataIndex: 'gsz',
  },
  {
    title: 'gszzl',
    dataIndex: 'gszzl',
  },
  {
    title: 'gztime',
    dataIndex: 'gztime',
  },
];

export class FundTable extends Component {

    state = {
      data: [],
      loading: false,
    };

    // 构造方法 
    // this.props 为组件传参
    constructor() {
      super()
    }

    handleTableChange = () =>{
      // this.fetch(codes=["001182"])
      this.fetch({codes:this.props.numbers})
    }
    
    fetch = async ({codes}) => {
      this.setState({ loading: true });
      
      var rows = []
      for(var i=0;i<codes.length;i++){
        console.log(codes[i])
        await fund.fetchData(codes[i]).then((res)=>{
          console.log(res)
          res["key"] = res["fundcode"]
          rows.push(res)
        }).catch((err)=>{
          console.log("error:")
          console.log(err)
        })
      }

      this.setState({
        loading: false,
        data: rows
      });

    };

    // 渲染之前执行
  componentWillMount() {
      /*
        该方法可以用于一些数据的提前加载
      */
    }

  createData(name, code, population, size) {
    const density = population / size;
    return { name, code, population, size, density };
  }

  render() {
    const { data, loading } = this.state;
    return (
      <div>
        <Button onClick={this.handleTableChange}> 获取数据 </Button>
        <Table pagination={false} dataSource={data} columns={columns} loading={loading} onChange={this.handleTableChange} />
      </div>
    )
  }

  // 渲染之后执行
  componentDidMount() {
    /*
      该方法可以用于清除一些无效的数据
    */
  }

 }