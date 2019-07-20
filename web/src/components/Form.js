import React, {Component} from "react";
import PropTypes from "prop-types";

class Form extends Component {
    static propTypes = {
        endpoint: PropTypes.string.isRequired
    };

    state = {
        pod_name: "",
        pod_log: {lines: "No logs selected \n Yet"},
        yaml_url: "",
        noti: ""
    };

    handleChangeGetLog = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    handleSubmitGetLog = e => {
        e.preventDefault();
        const {pod_name, pod_log} = this.state;
        const pod = {
            pod_name,
            pod_log
        };
        const conf = {
            method: "get",
            headers: new Headers({
                "Content-Type": "application/json"
            })
        };
        // fetch(this.props.endpoint, conf).then(response => console.log(response));
        fetch(this.props.endpoint + "pod_log/?pod_name=" + pod.pod_name, conf)
            .then(response => response.json())
            .then(data =>
                this.setState({
                    pod_log: data
                })
            )
            .catch(error => console.error(error));
    };

    handleChangeCreate = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    handleSubmitCreate = e => {
        e.preventDefault();
        const {yaml_url} = this.state;
        const yaml_obj = {yaml_url};
        const conf = {
            method: "post",
            body: JSON.stringify(yaml_obj),
            headers: new Headers({"Content-Type": "application/json"})
        };

        const notification = (
            <div className="notification is-primary">
                <button className="delete"></button>
                Successfully Created!
            </div>
        );


        fetch(this.props.endpoint + "apply_yaml/", conf).then(
            response => {
                if (response.ok) {
                    this.setState({noti: notification});
                }
            });
        console.log(this.state);

        // Vanila JS to delete all notifications
        document.addEventListener('DOMContentLoaded', () => {
            (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
                $notification = $delete.parentNode;
                $delete.addEventListener('click', () => {
                    $notification.parentNode.removeChild($notification);
                });
            });
        });
    };


    render() {
        const {pod_name, yaml_url, noti} = this.state;
        return (
            <div className="tile is-parent is-vertical">
                {noti}

                <div className="tile is-child box">
                    <form onSubmit={this.handleSubmitCreate}>
                        <div className="field tile is-vertical">
                            <label className="label"> Create by File </label>
                            <div className="control">
                                <input className="input" name="yaml_url" type="text" onChange={this.handleChangeCreate}
                                       value={yaml_url} id="yaml-url-input" required/>
                            </div>
                        </div>
                        <div className="control">
                            <button id="yaml-url-submit" type="submit"
                                    className="button is-primary is-medium is-fullwidth is-rounded is-outlined">Create
                            </button>
                        </div>
                    </form>
                </div>

                <div className="tile is-child box">
                    <form onSubmit={this.handleSubmitGetLog}>
                        <div className="field tile is-vertical">
                            <label className="label"> PodName </label>
                            <div className="control">
                                <input className="input" type="text" name="pod_name" onChange={this.handleChangeGetLog}
                                       value={pod_name} required/>
                            </div>
                        </div>
                        <div className="control">
                            <button type="submit"
                                    className="button is-info is-medium is-fullwidth is-rounded is-outlined">Get Log
                            </button>
                        </div>
                    </form>
                </div>

                <div className="tile is-child box">
                    <p className="title">Logs...</p>
                    <div>
                        {this.state.pod_log.lines.split("\n").filter(l => l.includes('Pi is')).map((i, key) => {
                            return <div key={key}>{i}</div>;
                        })}
                    </div>
                </div>
            </div>

        );
    }
}

export default Form;
