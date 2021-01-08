import React, { Component } from 'react'
import '../NavBar/navbar.css'
import './alert.css'

export default class Alert extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
            open: false
        }
    }

    handleOpen = () => {
        this.props.changeMarkerState(true)
        this.setState({
            open: true
        })
        this.props.reset()
    }

    render() {
        return (
            <div>
                <div onClick={this.handleOpen} id="alert-casing">
                    <span style={{fontSize: "30px"}} className="material-icons material-styling">
                        local_fire_department
                    </span>
                </div>
            </div>
        )
    }
}
