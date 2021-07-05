// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity 0.6.12;

interface IRewards {
    function notifyRewardAmount(uint256 reward) external;

    function earned(address account) external view returns (uint256);

    function stake(uint256 amount) external;

    function withdraw(uint256 amount) external;

    function exit() external;

    function getReward() external;

    function balanceOf(address account) external view returns (uint256);

    function DURATION() external view returns (uint256);

    function starttime() external view returns (uint256);

    function periodFinish() external view returns (uint256);
}
