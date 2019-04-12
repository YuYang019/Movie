import React, { Component } from 'react';
import Rating from './page/Rating';
import Result from './page/Result';
import Welcome from './page/Welcome';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import './App.css';

import { Button } from 'antd';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Route path="/" exact component={Welcome} />
          <Route path="/rating/" component={Rating} />
          <Route path="/result/" component={Result} />
        </div>
      </Router>
      
    );
  }
}

export default App;
