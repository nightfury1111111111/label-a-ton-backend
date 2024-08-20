//user Controllers
export {home as home} from "./user";
export {increaseCoins as increaseCoins} from "./user";
export {decreaseCoins as decreaseCoins} from "./user";

// Airdrop Controllers
export {leaderBoard as leaderBoard} from "./airdrop";
export {addFriend as addFriend} from "./airdrop";

//Auth Controllers
export {signin as signinController} from "./auth";
export {signup as signupController} from "./auth";

//Workforce Controllers
export {agentJobBoard as agentJobBoard} from "./workforce";
export {assignJob as assignJob} from "./workforce";
export {unassignJob as unassignJob} from "./workforce";
export {assignAgent as assignAgent} from "./workforce";
export {buyData as buyData} from "./workforce";
export {buyGpu as buyGpu} from "./workforce";

//Earn Controllers
export {earnBoard as earnBoard} from "./earn";
export {executeTask as executeTask} from "./earn";
export {processBalance as processBalance} from "./earn";

//Agents Controllers
export {agentsList as agentsList} from "./agents";
export {agentsPair as agentsPair} from "./agents";
export {agentCreate as agentCreate} from "./agents";
export {agentUpgrade as agentUpgrade} from "./agents";