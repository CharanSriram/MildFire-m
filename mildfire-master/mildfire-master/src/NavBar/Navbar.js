import React, {useState} from 'react';
import './navbar.css'

export default function Navbar(props) {
    return (
        <div id="nav-container">
            <div className="nav-buttons" id="home">
                <span className="material-icons material-styling">
                    notifications
                </span>
            </div>
            <div id="search"></div>
            <div onClick={() => props.reset()} className="nav-buttons" id="reset">
                <span className="material-icons material-styling">
                    my_location
                </span>
            </div>
        </div>
    )
    
}
