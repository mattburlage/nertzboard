import React, {Component} from 'react';
import Container from "reactstrap/es/Container";
import PointsForm from "./PointsForm/PointsForm";
import GameInfo from "./GameInfo/GameInfo";
import GameTable from "./GameTable/GameTable";
import Spinner from "reactstrap/es/Spinner";
import apiUrl from "../../assets/apiUrl";

let myTimer;

class Gameboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            roomData: {},
            rounds: {},
            autoRefresh: false,
        };
        this.updateScores = this.updateScores.bind(this);
        this.toggleAutoRefresh = this.toggleAutoRefresh.bind(this);
    }

    componentDidMount() {
        this.updateScores()
    }

    updateScores() {
        console.log('Update Scores');
        fetch(apiUrl + '/nertz/current_game_data/', {
            headers: {
                Authorization: `JWT ${localStorage.getItem('token')}`
            }
        })
            .then(res => res.json())
            .then(json => {
                this.setState({
                    roomData: json.room_data,
                    rounds: json.rounds,
                    isLoaded: true,
                });
            });
    }

    toggleAutoRefresh () {
        console.log('toggleAutoRefresh', this.state.autoRefresh);
        if (this.state.autoRefresh) {
            this.setState({
                autoRefresh: false,
            });
            clearInterval(myTimer)
        } else {
            this.setState({
                autoRefresh: true,
            });
            myTimer = setInterval(this.updateScores, 5000)
        }
    }

    render() {
        if (!this.state.isLoaded && false) {
            return (
                <div className={'mt-5 text-center'}><Spinner type={'grow'} color={'primary'} /><br/>Loading</div>
            )
        }

        return (
            <Container className='mt-3'>
                <GameInfo roomData={this.state.roomData}/>
                <PointsForm
                    handleUpdate={this.updateScores}
                />
                <GameTable gameData={this.state.rounds}
                           maxRounds={this.state.roomData.max_rounds}
                           darkMode={this.props.darkMode}
                           handleRefresh={this.updateScores}
                           toggleAutoRefresh={this.toggleAutoRefresh}
                           autoRefresh={this.state.autoRefresh}
                />
            </Container>
        );
    }
}

export default Gameboard;
