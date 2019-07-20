import React, {Component} from "react";
import PropTypes from "prop-types";

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
};

const repeat = (milliseconds) => {
    return this.interval = setInterval(() => this.setState({ time: Date.now() }), 1000)
};

class DataProvider extends Component {
    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        render: PropTypes.func.isRequired
    };

    state = {
        data: [],
        loaded: false,
        placeholder: "Loading..."
    };

    componentDidMount() {
        sleep(500).then(() => {
        fetch(this.props.endpoint)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                return response.json();
            })
            .then(data => this.setState({data: data, loaded: true}));
        })
    };

    render() {

            const {data, loaded, placeholder} = this.state;
        return loaded ? this.props.render(data) : <p> {placeholder} </p>;

}
}


    export default DataProvider;
