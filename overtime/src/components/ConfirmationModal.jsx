import React from 'react'
import axios from 'axios'
const ConfirmationModal = (props) => {
    
    const {formValues, setOpenModal, setSuccess, setFormValues} = props
    const {EMPLOYEE_NO, WORK_ORD_NO, OVT_DATE, DUTY_DESC, START_HR, END_HR, OVT_DAY} = formValues

    const handleSubmit = async () => {
        try{
            let response = await axios.post("http://localhost:8080/api/ovt_entries", formValues, {
              method: 'POST',
              headers: {
                      'Content-Type': 'application/json',
            },
            })
            console.log(response)
            console.log(response.data)
            if(response.status === 200 || 201){
                setSuccess("Form submitted successfully")
            }
            setFormValues("")
          }catch(error){
            console.log(error)
          }
    }
    return (
    <section className='modal_section'>
    <div className="inner-overlay">

        <div className="flex justify-between items-center my-10">
        <h3>Form Preview</h3>
        <button className='modal_close_btn font-extrabold' onClick={()=>setOpenModal(false)}>X</button>
        </div>
    <div className='confirmation_modal_table'>
    <table>
        <thead>
            <th>Employee No</th>
            <th>Date</th>
            <th>Overtime Day</th>
            <th>Description of Duties</th>
            <th>Overtime from</th>
            <th>Overtime to</th>
            <th>Work Order No</th>
        </thead>
        <tbody>
            <tr>
                <td>{EMPLOYEE_NO}</td>
                <td>{OVT_DATE}</td>
                <td>{OVT_DAY}</td>
                <td>{DUTY_DESC}</td>
                <td>{START_HR}</td>
                <td>{END_HR}</td>
                <td>{WORK_ORD_NO}</td>
            </tr>
        </tbody>

    </table>
    <div className='modal_btn'>
    <button className='cancel_btn' onClick={()=> setOpenModal(false)}>cancel</button>
    <button className='submit_btn' type='submit' onClick={handleSubmit} >submit</button>
    </div>
    </div>
    </div>

    </section>
  )
}

export default ConfirmationModal