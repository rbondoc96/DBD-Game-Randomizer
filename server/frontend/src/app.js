import React from "react"
import ReactDOM from "react-dom"
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

// Partials
// import NavBar from "./components/navbar"
// import Footer from "./components/footer"

// Views
// import Home from "./views/home"
// import Error404 from "./views/error-404"

export default function App(props) {
    return(
        <Router>
            <div className="app">
            hI
                <Switch>
                    {/* <Route exact path="/" component={Home} />
                    <Route path="*" component={Error404} /> 404 page */}
                </Switch>
            </div>
        </Router>
    )
}