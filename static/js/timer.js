const STATUS_ENDPOINT = "/api/timer/status";
const START_ENDPOINT = "/api/timer/start";
const RESET_ENDPOINT = "/api/timer/reset";
const TODAY_STATS_ENDPOINT = "/api/sessions/today";

const POLL_INTERVAL_MS = 1000;

document.addEventListener("DOMContentLoaded", () => {
	const statusElement = document.querySelector("[data-timer-status]");
	const displayElement = document.querySelector("[data-timer-display]");
	const completedSessionsElement = document.querySelector("[data-completed-sessions]");
	const totalFocusElement = document.querySelector("[data-total-focus]");
	const startButton = document.querySelector('[data-action="start"]');
	const resetButton = document.querySelector('[data-action="reset"]');

	async function fetchStatus() {
		try {
			const response = await fetch(STATUS_ENDPOINT, { cache: "no-store" });
			if (!response.ok) throw new Error("Failed to fetch status");
			const data = await response.json();
			updateTimerDisplay(data);

			if (data.state === "completed") {
				await fetchSessionStats();
			}
		} catch (error) {
			console.error(error);
		}
	}

	async function fetchSessionStats() {
		try {
			const response = await fetch(TODAY_STATS_ENDPOINT, { cache: "no-store" });
			if (!response.ok) throw new Error("Failed to fetch session stats");
			const stats = await response.json();
			updateSessionStats(stats);
		} catch (error) {
			console.error(error);
		}
	}

	function updateTimerDisplay(data) {
		if (statusElement) {
			statusElement.textContent = data.status_label ?? "";
		}
		if (displayElement) {
			displayElement.textContent = data.display_time ?? formatMmSs(data.remaining_seconds ?? 0);
		}
	}

	function updateSessionStats(stats) {
		if (completedSessionsElement) {
			completedSessionsElement.textContent = stats.completed_sessions ?? 0;
		}
		if (totalFocusElement) {
			totalFocusElement.textContent = stats.display_focus_time ?? "0分";
		}
	}

	async function startTimer() {
		try {
			const response = await fetch(START_ENDPOINT, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ session_type: "work" }),
			});
			if (!response.ok) throw new Error("Failed to start timer");
			const data = await response.json();
			updateTimerDisplay(data);
		} catch (error) {
			console.error(error);
		}
	}

	async function resetTimer() {
		try {
			const response = await fetch(RESET_ENDPOINT, { method: "POST" });
			if (!response.ok) throw new Error("Failed to reset timer");
			const data = await response.json();
			updateTimerDisplay(data);
		} catch (error) {
			console.error(error);
		}
	}

	function formatMmSs(totalSeconds) {
		const seconds = Math.max(0, Number(totalSeconds) || 0);
		const minutes = Math.floor(seconds / 60);
		const remainder = seconds % 60;
		return `${minutes.toString().padStart(2, "0")}:${remainder.toString().padStart(2, "0")}`;
	}

	if (startButton) {
		startButton.addEventListener("click", startTimer);
	}
	if (resetButton) {
		resetButton.addEventListener("click", resetTimer);
	}

	fetchStatus();
	fetchSessionStats();
	setInterval(fetchStatus, POLL_INTERVAL_MS);
});
