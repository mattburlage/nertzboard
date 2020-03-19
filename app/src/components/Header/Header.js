import React from 'react';
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem } from 'reactstrap';
import apiUrl from "../../assets/apiUrl";

export default class Header extends React.Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false,
        };
        this.toggleDarkMode = this.toggleDarkMode.bind(this);
        this.handle_logout = this.handle_logout.bind(this);
    }
    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    toggleDarkMode() {
        this.setState({
            isOpen: false,
        });
        this.props.toggleDarkMode()
    }

    handle_logout(e) {
        e.preventDefault();
        this.setState({
            isOpen: false,
        });
        this.props.handle_logout()
    }

    render() {
        let adminLink = (
            <div />
        );

        if (this.props.superUser) {
            adminLink = (
                <NavItem>
                    <NavLink href={apiUrl + "/admin"}>Admin</NavLink>
                </NavItem>
            )
        }

        let navbarClasses = this.props.darkMode ? 'navbar-dark bg-dark' : 'navbar-light';

        if (!this.props.loggedIn) {
            return (
                <div>
                    <Navbar className={navbarClasses} expand="md">
                        <NavbarBrand>NertzBoard</NavbarBrand>
                        <NavbarToggler onClick={this.toggle} />
                        <Collapse isOpen={this.state.isOpen} navbar>
                            <Nav navbar>
                                <NavItem>
                                    <NavLink href="/">Log In</NavLink>
                                </NavItem>
                            </Nav>
                        </Collapse>
                    </Navbar>
                </div>
            )
        }

        return (
            <div>
                <Navbar className={navbarClasses} expand="md">
                    <NavbarBrand>NertzBoard</NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav navbar>
                            <NavItem>
                                <NavLink href="/">Current Game</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/">Statistics</NavLink>
                            </NavItem>
                            <UncontrolledDropdown nav inNavbar>
                                <DropdownToggle nav caret>
                                    Options
                                </DropdownToggle>
                                <DropdownMenu right>
                                    <DropdownItem>
                                        New Game
                                    </DropdownItem>
                                    {/*<DropdownItem>*/}
                                    {/*    Leave Game*/}
                                    {/*</DropdownItem>*/}
                                    {/*<DropdownItem>*/}
                                    {/*    Switch Room*/}
                                    {/*</DropdownItem>*/}
                                    <DropdownItem divider />
                                    <DropdownItem onClick={this.toggleDarkMode}>
                                        Toggle Dark Mode
                                    </DropdownItem>
                                </DropdownMenu>
                            </UncontrolledDropdown>
                            {adminLink}
                            <NavItem>
                                <NavLink href='/' onClick={this.handle_logout}>Log Out</NavLink>
                            </NavItem>
                        </Nav>
                        <Nav navbar className={'ml-auto'}>
                            <NavItem className={'navbar-text'}>
                                Signed in as {this.props.username}
                            </NavItem>

                        </Nav>

                    </Collapse>
                </Navbar>
            </div>
        );
    }
}
