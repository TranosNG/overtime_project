import React from 'react'
import Header from './Header/Header'
import OvertimeTable from '../pages/OvertTimeTable'
import OverTimeForm from '../pages/OverTimeForm/OverTimeForm'
const UserDashboard = () => {
  return (
    <>
    <Header/>
    <OverTimeForm/>
    <OvertimeTable/>
    </>
  )
}

export default UserDashboard