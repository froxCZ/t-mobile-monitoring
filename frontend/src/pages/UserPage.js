import React, {Component, PropTypes} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import Button from 'react-bootstrap/lib/Button';
import Panel from 'react-bootstrap/lib/Panel';
import Pagination from 'react-bootstrap/lib/Pagination';
import PageHeader from 'react-bootstrap/lib/PageHeader';
import {performFetchPromise} from '../actions/ApiRequest'
import {showLoading, hideLoading} from 'react-redux-loading-bar'

function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}

class UserPage extends Component {

  constructor() {
    super();
    this.state = {
      users: []
    };
  }

  componentWillMount() {
    this.fetchUsers();
  }

  fetchUsers() {
    var myInit = {
      method: 'GET'
    };
    var that = this;
    this.props.showLoading();
    performFetchPromise("/user", myInit).then(result => {
      that.setState({users: result});
      that.props.hideLoading();
    });

  }

  render() {
    var userRows = this.state.users.map(user =>
      <tr className="gradeA odd" role="row">
        <td className="sorting_1">{user._id}</td>
        <td>{user.name}</td>
        <td>asd</td>
      </tr>
    );
    console.log(userRows);
    return <div>
      <div className="col-lg-12">
        <PageHeader>Users</PageHeader>
      </div>

      <div className="col-lg-12">
        <Panel header={<span>List of users</span>}>
          <div>
            <div className="dataTable_wrapper">
              <div
                id="dataTables-example_wrapper"
                className="dataTables_wrapper form-inline dt-bootstrap no-footer"
              >

                <div className="row">
                  <div className="col-sm-3">
                    <div id="dataTables-example_filter" className="dataTables_filter">
                      <label htmlFor={'search'}>Search:
                        <input
                          type="search"
                          className="form-control input-sm"
                          placeholder=""
                          aria-controls="dataTables-example"
                          id="search"
                        />
                      </label>
                    </div>
                  </div>
                </div>

                <div className="row">
                  <div className="col-sm-12">
                    <table
                      className="table table-striped table-bordered table-hover dataTable no-footer"
                      id="dataTables-example"
                      role="grid"
                      aria-describedby="dataTables-example_info"
                    >
                      <thead>
                      <tr role="row">
                        <th
                          tabIndex="0"
                          rowSpan="1"
                          colSpan="1"
                          style={{width: 265}}>
                          Username
                        </th>
                        <th
                          tabIndex="0"
                          rowSpan="1"
                          colSpan="1"
                          style={{width: 265}}>
                          Name
                        </th>
                        <th
                          tabIndex="0"
                          rowSpan="1"
                          colSpan="1"
                          style={{width: 265}}>
                          Roles
                        </th>
                      </tr>
                      </thead>
                      <tbody>
                      {userRows}

                      </tbody>
                    </table>
                  </div>
                </div>
                <div className="row">
                  <div className="col-sm-6">
                    <div
                      className="dataTables_info"
                      id="dataTables-example_info"
                      role="status"
                      aria-live="polite"
                    >
                      Showing 1 to 10 of 57 entries
                    </div>
                  </div>
                  <div className="col-sm-6 pullRight ">
                    <Pagination
                      activePage={1}
                      items={6}
                      first
                      last
                      prev
                      next
                      onSelect={() => {
                        // function for Pagination
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Panel>
      </div>

      <div className="row ng-scope">

      </div>


    </div>
  }
}
UserPage = connect(mapStateToProps, mapDispatchToProps)(UserPage)
export default UserPage