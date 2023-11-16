import React from 'react'
import './Header.css'
import logo from '../../images/tranos_logo.png'
// import { Link } from 'react-router-dom'


const Header = () => {
  return (
    <header className='header_section'>
        
        <div className='logo'>
      <img src={logo} alt={logo} />
      </div>
        
        
        {/* <div className='sign_up_btn_div'>
        <Link to="/signUp"><button className='sign_up_btn' type='button'>Sign up </button>
        <Link to="/logIn"><button className='log_in_btn' type='button'>log in </button></Link>
        </Link> 
        </div>*/}

    </header>
  )
}

export default Header