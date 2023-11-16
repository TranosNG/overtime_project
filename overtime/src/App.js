import OverTimeForm from "./pages/OverTimeForm/OverTimeForm";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SignInForm from "./components/RegisterForm/SignInForm";
import SignUpForm from "./components/RegisterForm/SignUpForm";
import OvertimeTable from "./pages/OvertTimeTable";
// import UserDashboard from "./components/UserDashboard";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/overtime_form" element={<OverTimeForm/>}/>
        <Route path="/signUp" element={<SignUpForm/>}/>
        <Route path="/logIn" element={<SignInForm/>}/>
        <Route path="/user_dashboard" element={<OvertimeTable/>}/>
        {/* <Route path="/user_dashboard" element={<UserDashboard/>}/> */}
      </Routes>
    </div>
  );
}

export default App;
