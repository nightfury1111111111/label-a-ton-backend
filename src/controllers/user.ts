/**
 * User Controller
 *
 * @since 1.0.0
 * @version 1.0.0
 */

import express, { Request, Response } from "express";
import axios from "axios";
import User from "../models/user";

import assert from "assert";
import bs58 from "bs58";

function wait(milliseconds: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });
}

class UserController {
  public async test(req: Request, res: Response) {
    console.log("user controller is working");
    res.send("ok");
  }
}

export default UserController;
