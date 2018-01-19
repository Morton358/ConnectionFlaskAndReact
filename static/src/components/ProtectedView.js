import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as actionCreators from '../actions/data';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import axios from 'axios';

function mapStateToProps(state) {
    return {
        data: state.data,
        token: state.auth.token,
        loaded: state.data.loaded,
        isFetching: state.data.isFetching,
    };
}


function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
export default class ProtectedView extends React.Component {
  state = {
    lindoapi: '',
  }

    componentDidMount() {
        this.fetchData()
        axios.get('/api/calculate')
        .then(response => {
          this.setState({lindoapi: response.data})
          console.log(response);
        });
    }


    fetchData() {
        const token = this.props.token;
        this.props.fetchProtectedData(token);
    }

    render() {
        return (
            <div>
                {!this.props.loaded
                    ? <h1>Loading data...</h1>
                    :
                    <div>
                        <h1>Welcome back,
                            {this.props.userName}!</h1>
                        <h1>{this.props.data.data.email}</h1>
                        <RaisedButton
                          label="Calculate"
                          primary={true}
                          onClick="" />
                          <Card>
                            <CardHeader
                              title="Objective value is:"
                              actAsExpander={true}
                            />
                            <CardText expandable={true}>
                              {this.state.lindoapi.objective}
                            </CardText>
                          </Card>
                    </div>
                }
            </div>
        );
    }
}

ProtectedView.propTypes = {
    fetchProtectedData: React.PropTypes.func,
    loaded: React.PropTypes.bool,
    userName: React.PropTypes.string,
    data: React.PropTypes.any,
    token: React.PropTypes.string,
};
