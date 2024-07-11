/**
 * User model
 *
 * @since 1.0.0
 * @version 1.0.0
 * @package main/Models/Users
 */

import mongoose from "mongoose";

const UserSchema = new mongoose.Schema(
  {
    name: {
      type: String,
    },
    profileImage: {
      type: String,
    },
    note: {
      type: String,
    },
    // ... need to add more info
  },
  {
    timestamps: {
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  }
);

const model = mongoose.models.User || mongoose.model("User", UserSchema);

export default model;
