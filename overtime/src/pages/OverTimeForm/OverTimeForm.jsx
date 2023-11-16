import React, {useState} from 'react'
import { Formik, Form, Field, ErrorMessage} from 'formik';
import * as Yup from 'yup';
import ConfirmationModal from '../../components/ConfirmationModal';
import './OverTimeForm.css'


const OverTimeForm = (props) => {
  const {usersNo} = props
  const [success, setSuccess] = useState('')
  const [formValues, setFormValues] = useState("")
  const [openModal, setOpenModal] = useState(false)
  const validationSchema = Yup.object({
    EMPLOYEE_NO: Yup.string().required('Employee No is required'),
    OVT_DAY: Yup.string().required('Day is required '),
    DUTY_DESC: Yup.string().required('Duty description is required'),
    OVT_DATE: Yup.string().required('Date is required'),
    START_HR: Yup.string().required('Overtime duration is required'),
    END_HR: Yup.string().required('Overtime duration is required'),
    WORK_ORD_NO: Yup.string().required('Work order No is required'),
  });
  const initialValues = {
    EMPLOYEE_NO: '',
    OVT_DAY: '',
    DUTY_DESC: [],
    OVT_DATE: '',
    START_HR: '',
    END_HR: '',
    WORK_ORD_NO: []
  };
  
const handleSubmit = async (values) => {
  setFormValues(values)
  console.log(values)
  setOpenModal(!openModal)
}  

  return (
    <>
    <section className='overtime_section'>
      <h3>OverTime Payment Form</h3>
      <div className='overtime_form_container'>
      <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={(values)=>handleSubmit(values)}
    >
      <Form>
      <h3 style={{color: "green"}}>{success}</h3>
         <div className='form-group'>
        <div className='flex-1 mr-3'>
          <div className='md:flex items-center'>
            <div className='flex-1'>
          <label htmlFor="EMPLOYEE_NO">Employee No</label>
          <Field type="text" id="EMPLOYEE_NO" name="EMPLOYEE_NO" placeholder="enter your employee no" value={usersNo}/>
          <ErrorMessage style={{color: "red"}} name="EMPLOYEE_NO" component="div" />
          </div>

          <div className='md:flex-1 md:ml-3  md:w-10'>
          <label htmlFor="OVT_DAY">Overtime Day</label>
          <Field id="OVT_DAY" name="OVT_DAY" as="select">
            <option disabled value="">Overtime Day</option>
            <option value="Sunday">Sunday</option>
            <option value="Monday">Monday</option>
            <option value="Tueday">Tueday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thurday">Thursday</option>
            <option value="Friday">Friday</option>
            <option value="Saturday">Saturday</option>
            
          <ErrorMessage style={{color: "red"}} name="overtime_day" component="div"/>
          </Field>
          </div>
          </div>
        </div> 

        </div>

        <div className='form-group'>
        <div className='flex-1 mr-3'>
          <label htmlFor="time">Time of Overtime</label>
          <div className='md:flex'>
          <Field className='md:mr-3 mb-5' type="time" id="START_HR" name="START_HR" placeholder="start hour"/>
          <Field className="mb-5" type="time" id="END_HR" name="END_HR" placeholder="end hour"/>
          </div>
          <ErrorMessage style={{color: "red"}} name="time" component="div" />
        </div>

        <div className='flex-1 mr-3'>
          <label htmlFor="OVT_DATE">Date of Overtime</label>
          <Field type="date" id="OVT_DATE" name="OVT_DATE" placeholder="enter date of overtime"/>
          <ErrorMessage style={{color: "red"}} name="OVT_DATE" component="div" />
        </div>
        </div>

        
        <div className='form-group'>
        <div className='flex-1 mr-3'>
          <label htmlFor="DUTY_DESC">Description of Duties</label>
          <Field type="text" id="DUTY_DESC" name="DUTY_DESC" placeholder="describe your duties"/>
          <ErrorMessage style={{color: "red"}} name="DUTY_DESC" component="div" />
        </div>

        </div>

        
        <div className='flex-1 mr-3'>
          <label htmlFor="WORK_ORD_NO">Work Order Number</label>
          <Field type="text" id="WORK_ORD_NO" name="WORK_ORD_NO" component="textarea" placeholder="enter your work order no"/>
          <ErrorMessage style={{color: "red"}} name="WORK_ORD_NO" component="div" />
        </div>
        
        <button className='overtime_submit_btn' >Confirm</button>
    {openModal ? <ConfirmationModal handleSubmit={handleSubmit} formValues={formValues} openModal={openModal} setOpenModal={setOpenModal} success={success} setSuccess={setSuccess} setFormValues={setFormValues}/> : null}
      </Form>
    </Formik>
    </div>

    </section>
    </>
  )
}

export default OverTimeForm

