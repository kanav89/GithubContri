import React from 'react';
import { Link } from 'react-router-dom';
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Avatar} from "@nextui-org/react";

function Layout({ children, username,accessToken }) {
  return (
    <div className="flex flex-col min-h-full">
      <Navbar className="bg-black" >
        <NavbarBrand >
          <p className="font-bold text-white text-inherit">Contribution Analysis</p>
        </NavbarBrand>
        <NavbarContent className="hidden sm:flex gap-4" justify="center">
          <NavbarItem>
            <Link to={`/streakHistory?username=${username}`} className="text-white">
              Streak Analysis
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link to="/goals" className="text-white">
              Set goals
            </Link>
          </NavbarItem>
          <NavbarItem>
            <Link to={`/page?username=${username}&access_token=${accessToken}`} className="text-white">
              Contributions
            </Link>
          </NavbarItem>
        </NavbarContent>
        <NavbarContent justify="end">
          <Avatar
            isBordered
            as="button"
            className="transition-transform"
            color="secondary"
            name="Jason Hughes"
            size="sm"
            src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
          />
        </NavbarContent>
      </Navbar>
      <main>{children}</main>
    </div>
  );
}

export default Layout;