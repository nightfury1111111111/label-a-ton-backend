import mongoose, { Schema } from 'mongoose';  
import { FLOAT } from 'sequelize';

// Create a Schema corresponding to the document interface.  
const agentSchema: Schema = new Schema({  
    agentName: {type: String, required: true, default: "Agent1"},  
    level: { type: Number, required: true },  
    assignState: { type: String, default: null },
    strength: {type: Number, required: true, default: 0},
    agility: {type: Number, required: true, default: 0},
    intelligence: {type: Number, required: true, default: 0},
    passiveIncome: {type: Number, default: 1}
});  

// Create a Model from the schema.
const Agent = mongoose.model('Agent', agentSchema);

export default Agent;