import React from 'react';
import ReactDOM from 'react-dom';
import CustomNavbar from './components/CustomNavbar';
import Main from './components/Main';
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/index.css';


ReactDOM.render(
  <React.StrictMode>
    <>
      <Main />
    </>
  </React.StrictMode>,
  document.getElementById('root')
);
