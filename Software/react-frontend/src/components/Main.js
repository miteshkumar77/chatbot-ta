import React from "react";
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import InteractionWindow from "./InteractionWindow";
import InstructorDashboard from "./InstructorDashboard";
import CustomNavbar from "./CustomNavbar";
import Login from "./Login"

function Main(){
    return (
        <>
        <Router>
            <CustomNavbar />
            <Routes>
                <Route path="/" strict exact element={<InteractionWindow type='chat' />} />
                <Route path="/search" strict exact element={<InteractionWindow type='search' />} />
                <Route path="/login" strict exact element={<Login />} />
                <Route path="/instructor" strict exact element={<InstructorDashboard />} />
            </Routes>
        </Router>
        </>
        
    );
}

export default Main;