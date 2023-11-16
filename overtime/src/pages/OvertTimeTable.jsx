import React, { useEffect, useState} from 'react'
import axios from 'axios'
import OverTimeForm from './OverTimeForm/OverTimeForm'
import Header from '../components/Header/Header'


const OvertimeTable = () => {
  const [users, setUsers] = useState([])
  
    const fetchOvertimeRecords = async () => {
    const token = localStorage.getItem("token")
    const tokenParse = JSON.parse(token)
    try{
      let url = "http://localhost:8080/api/reg_entries"
      let response = await axios.get(url, {
        headers: {'Content-Type': 'application/json;charset=utf-8',
        Authorization: `Bearer ${tokenParse}`}
      })
      console.log(response)
      console.log(response.data)
      setUsers(response.data)
    }catch(error){
        console.log(error)
    }
  }
  useEffect(()=>{
    fetchOvertimeRecords()
  }, [])
  return (
    <>
    <Header/>
    <OverTimeForm usersNo={users.EMPLOYEE_NO}/>
    {users.length === 0 ? <p style={{color: "#3BC7F0"}} className='text-center text-xl'>No records found</p> : <table className='user_table_container'>
        <thead>
                <th>FIRSTNAME</th>
                <th>LASTNAME</th>
                <th>POSITION</th>
                <th>EMPLOYEE NO</th>
                <th>PHONE NO</th>
                <th>OVT DAY</th>
                <th>DUTY DESC</th>
                <th>OVT DATE</th>
                <th>START HR</th>
                <th>END HR</th>
                <th>WORK ORDER NO</th>
                <th>TOTAL HR WORKED</th>
                <th>TOTAL PAY AMT</th>
                
            </thead>
            <tbody>
                  {users.map((user)=>{
                    const {ID, FIRST_NAME, LAST_NAME, EMPL_POSITION, EMPLOYEE_NO, PHONE_NO, OVT_DAY, DUTY_DESC, OVT_DATE, START_HR, END_HR, WORK_ORD_NO, TOTAL_HR_WORKED, TOTAL_PAY_AMT} = user
                    let hrWorked = TOTAL_HR_WORKED.toFixed(2)
                    return(
                      <>
                      <tr key={ID}>
                    <td>{FIRST_NAME}</td>
                    <td>{LAST_NAME}</td>
                    <td>{EMPL_POSITION}</td>
                    <td>{EMPLOYEE_NO}</td>
                    <td>{PHONE_NO}</td>
                    <td>{OVT_DAY}</td>
                    <td>{DUTY_DESC}</td>
                    <td>{OVT_DATE}</td>
                    <td>{START_HR}</td>
                    <td>{END_HR}</td>    
                    {/* <td>{users.START_HR.slice(0, 5)}</td> */}
                    {/* <td>{users.END_HR.slice(0, 5)}</td>     */}
                    <td>{WORK_ORD_NO}</td>    
                    <td>{hrWorked}</td>    
                    <td>{TOTAL_PAY_AMT}</td> 
                    </tr>
                      </>
                    )
                  })}   
            </tbody> 
        </table> }
      
    </> 
  )
}

export default OvertimeTable