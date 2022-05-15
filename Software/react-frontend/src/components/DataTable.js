import React from 'react';
import Table from 'react-bootstrap/Table';
import "../css/table.css"

const DataTable = (props) => (
    <Table responsive striped bordered hover id="table" variant="primary">
        <thead>
            <tr>
                <th>#</th>
                <th>Query</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            {props.tableData.map((row, idx) => (
                <tr key={idx}>
                    <td>{idx + 1}</td>
                    <td>{row.query}</td>
                    <td>{row.timestamp}</td>
                </tr>
            ))}
        </tbody>
    </Table>
);

export default DataTable;