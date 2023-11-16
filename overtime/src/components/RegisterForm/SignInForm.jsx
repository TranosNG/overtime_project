import React, { useState} from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import './Register.css'
import { Link } from 'react-router-dom';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import Header from '../Header/Header';

const SignInForm = () => {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [succesSMessage, setSuccesSMessage] = useState('')
    const validationSchema = Yup.object({
      EMPLOYEE_NO: Yup.string().required('Employee No is required'),
        PWD: Yup.string().required('Password is required'),
      });
      const initialValues = {
        EMPLOYEE_NO: '',
        PWD: ''
      };
      const handleUsreSignIn = async (values) => {
        try{
          let url = 'http://localhost:8080/api/ovt_login'
          let response = await axios.post(url, values, {
            headers: {
                'Content-Type': 'application/json',
              },
            })
            localStorage.setItem("token", JSON.stringify(response.data[0].access_token))
            setSuccesSMessage("login successful")
        }catch(error){
          setError(error)
          console.log(error)
        }
        if(error.status === 200 || 201){
          setTimeout(()=>
          navigate('/user_dashboard'), 2000)
        }else if(error.status === 401 || 422){
          navigate(null)
          setError("Unauthorized user")
        }else if(error && error.status === 500){
          navigate(null)
          setError("Internal server Error, pleae try again later!")
        }
      }
  
  return (
    <>
      <Header/>
      <section className='signInForm_container'>

    <div>
      <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleUsreSignIn}
    >
    <Form className='sign_InForm'>
      <h3 className='font-semibold text-center'>Sign in </h3>
      <h3 className='text-center font-semi-bold' style={{color: "red"}}>{error}</h3>
      <h3 className='text-center font-semi-bold' style={{color: "green"}}>{succesSMessage}</h3>
      <div className='form_group'>
        <label htmlFor="EMPLOYEE_NO">Employee No</label>
        <Field type="text" id="EMPLOYEE_NO" name="EMPLOYEE_NO" placeholder="TRA_00560"/>
        <ErrorMessage style={{color: "red"}} name="EMPLOYEE_NO" component="div" />
    </div>

    <div className='form_group'>
        <label htmlFor="PWD">Password</label>
        <Field type="password" id="PWD" name="PWD" placeholder="enter your password"/>
        <ErrorMessage style={{color: "red"}} name="PWD" component="div" />
    </div>

    <button className='signIn_btn' type='submit'>Log in</button>
    <p className='text-center mt-3'>Don't have an account? <Link className='font-bold' to="/signUp" style={{color: "#303C7B"}}>Sign up</Link></p>
    </Form>
    </Formik>

      </div>  
    </section>
    </>
  )
}

export default SignInForm