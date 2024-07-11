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
    url: {
      type: String,
    },
    members: [
      {
        id: {
          type: mongoose.Schema.Types.ObjectId,
        },
      },
    ],
    commit: [
      {
        commitTime: Date,
        commitUrl: String,
        commitSummary: String,
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
