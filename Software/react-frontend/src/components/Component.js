import React from "react";
import Card from './Card';


export default (block, key) => {
    return React.createElement(Card, {
        key: key,
        block: block
    });
  };