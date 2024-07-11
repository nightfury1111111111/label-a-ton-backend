/**
 * User model
 *
 * @since 1.0.0
 * @version 1.0.0
 * @package main/Models/Users
 */

import mongoose from "mongoose";

const WorkspaceSchema = new mongoose.Schema(
  {
    name: {
      type: String,
    },
    members: [
      {
        id: { type: mongoose.Schema.Types.ObjectId },
        role: { type: String },
      },
    ],
    github: [
      {
        id: {
          type: mongoose.Schema.Types.ObjectId,
        },
        explanation: String,
      },
    ],
    // ... need to add more info
  },
  {
    timestamps: {
      createdAt: "created_at",
      updatedAt: "updated_at",
    },
  }
);

const model =
  mongoose.models.Workspace || mongoose.model("Workspace", WorkspaceSchema);

export default model;
