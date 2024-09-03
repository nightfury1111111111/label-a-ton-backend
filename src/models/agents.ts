import mongoose, { Schema } from 'mongoose';

// Create a Schema corresponding to the document interface.
const agentSchema = new Schema({  
    agentName: {type: String, required: true, default: "New Agent"},  
    level: { type: Number, required: true, default: 1 },
    assignState: { type: Boolean, default: true },
    strength: {type: Number, required: true, default: 0},
    agility: {type: Number, required: true, default: 0},
    survivability: {type: Number, required: true, default: 0},
    healthPoint: {type: Number, required: true, default: 0},
    passiveIncome: {type: Number, default: 1},
    jobId:[{   type: mongoose.Schema.Types.ObjectId,  ref: 'Task'}]
});  

// Create a Model from the schema.
const Agent = mongoose.model('Agent', agentSchema);

export default Agent;