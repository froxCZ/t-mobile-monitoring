import React, {Component} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";

function mapStateToProps(state) {
    return {auth:state.auth};
}
function mapDispatchToProps(dispatch) {
    return bindActionCreators({}, dispatch);
}

class Home extends Component {

    constructor() {
        super();
    }

    render() {
        return <div>Welcome {this.props.auth.user.name}</div>
    }
}
Home = connect(mapStateToProps, mapDispatchToProps)(Home)
export default Home