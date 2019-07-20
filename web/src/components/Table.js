import React from "react";
import PropTypes from "prop-types";
import key from "weak-key/index";

const Table = ({data}) =>
    !data.length ? (
            <div className="notification is-warning">
                Nothing to show
            </div>

        ) :
(
<div className = "tile is-parent" >
    <article className="tile is-child notification">
    <p className = "title" >
    Showing < strong > {data.length} items < /strong >
    </p>
        <font color="black">
        <table className = "table is-stripedc content" >
        <thead >
        <tr >
    {
        Object.entries(data[0]).map(el => < th key = {key(el)} > {el[0]} < /th>)}
        </tr>
        </thead>
        <tbody >
        {
            data.map(el => (
                < tr key = {el.id} >
            {
                Object.entries(el).map(el => < td key = {key(el)} > {el[1]} < /td>)}
                </tr>
))
}
        </tbody>
        </table> </font>
    </article>
</div>
);
Table.propTypes = {
    data: PropTypes.array.isRequired
};
export default Table;