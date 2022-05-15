import React from "react";
import Card from "react-bootstrap/Card";

export default props => (
    

    <Card bg="dark" text="light">
        <Card.Body>
            <Card.Title>{props.block.heading}</Card.Title>
            <Card.Subtitle className="mb-2 text-muted">{props.block.answer_text}</Card.Subtitle>
            <Card.Text>
                {props.block.surrounding_context_text[0]}<mark>{props.block.surrounding_context_text[1]}</mark>{props.block.surrounding_context_text[2]}
            </Card.Text>
            <Card.Link href={props.block.url}>Wiki Link</Card.Link>
        </Card.Body>
    </Card>
);