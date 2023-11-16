import React, {useState} from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import './Register.css'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import Header from '../Header/Header';

const SignUpForm = () => {
  const [succesSMessage, setSuccesSMessage] = useState('')
  const navigate = useNavigate()
  const handleUserReg = async (values) => {
    try{
      let url = 'http://localhost:8080/api/ovt_reg'
      let response = await axios.post(url, values, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
          },
      })
      setSuccesSMessage("Registration successful")
      console.log(response.data)
      // console.log(response.data.message)
    }catch(error){
      console.log(error)
    }
    setTimeout(()=>
    navigate('/login'),2000
    )
  } 
    

    const validationSchema = Yup.object({
        FIRST_NAME: Yup.string().required('First Name is required'),
        LAST_NAME: Yup.string().required('Last Name is required'),
        EMPL_POSITION: Yup.string().required('Position is required'),
        EMPLOYEE_NO: Yup.string().required('Employee No is required'),
        PHONE_NO: Yup.string().required('Phone number is required'),
        PWD: Yup.string().required('Password is required'),
        COFM_PWD: Yup.string().required("Password does not match")
        .oneOf([Yup.ref("PWD")], "Password does not match"),
      });
      const initialValues = {
        FIRST_NAME: '',
        LAST_NAME: '',
        EMPL_POSITION: '',
        EMPLOYEE_NO: '',
        PHONE_NO: '',
        PWD: '',
        COFM_PWD: ''
      };
      
  return (
    <>
    <Header/>
    <section className='signUpForm_container'>
      <h3 className='text-center' style={{color: "green"}}>{succesSMessage}</h3>
      <h3 className='font-semibold text-center'>Create an account</h3>
        <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleUserReg}
    >
    <Form className='sign_UpForm'>
    <div className='form_group'>
        <label htmlFor="FIRST_NAME">First Name</label>
        <Field type="text" id="FIRST_NAME" name="FIRST_NAME" placeholder="enter your first name"/>
        <ErrorMessage style={{color: "red"}} name="FIRST_NAME" component="div" />
    </div>


    <div className='form_group'>
        <label htmlFor="LAST_NAME">Last Name</label>
        <Field type="text" id="LAST_NAME" name="LAST_NAME" placeholder="enter your last name"/>
        <ErrorMessage style={{color: "red"}} name="LAST_NAME" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="EMPL_POSITION">Position</label>
        <Field type="text" id="EMPL_POSITION" name="EMPL_POSITION" placeholder="enter your position"/>
        <ErrorMessage style={{color: "red"}} name="EMPL_POSITION" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="EMPLOYEE_NO">Employee No</label>
        <Field type="text" id="EMPLOYEE_NO" name="EMPLOYEE_NO" placeholder="enter your employeeNo"/>
        <ErrorMessage style={{color: "red"}} name="EMPLOYEE_NO" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="PHONE_NO">Phone No</label>
        <Field type="text" id="PHONE_NO" name="PHONE_NO" placeholder="enter your phone number"/>
        <ErrorMessage style={{color: "red"}} name="PHONE_NO" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="PWD">Password</label>
        <Field type="password" id="PWD" name="PWD" placeholder="enter your password"/>
        <ErrorMessage style={{color: "red"}} name="PWD" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="COFM_PWD">Confirm Password</label>
        <Field type="password" id="COFM_PWD" name="COFM_PWD" placeholder="confirm password"/>
        <ErrorMessage style={{color: "red"}} name="COFM_PWD" component="div" />
    </div>
    <button className='signUp_btn' type='submit'>Submit</button>
    </Form>
    </Formik>
        
    </section>
    </>
  )
}

export default SignUpForm