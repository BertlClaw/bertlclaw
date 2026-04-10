#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const logPath = path.join(root, 'logs', 'bertlclaw-operations.log');
const statePath = path.join(root, 'state', 'bertlclaw-reminders.json');
const reportPath = path.join(root, 'qa-artifacts', 'reminder-audit', 'latest.json');

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function readText(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return '';
  }
}

function readJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return fallback;
  }
}

function nowVienna(date = new Date()) {
  const formatter = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'Europe/Vienna',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
  const parts = Object.fromEntries(formatter.formatToParts(date).filter(p => p.type !== 'literal').map(p => [p.type, p.value]));
  return {
    date: `${parts.year}-${parts.month}-${parts.day}`,
    hour: parts.hour,
    minute: parts.minute,
    second: parts.second,
    stamp: `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second} CEST`,
  };
}

function slotFor(date) {
  const p = nowVienna(date);
  return `${p.date} ${p.hour}:00`;
}

const argv = process.argv.slice(2);
const hoursFlag = argv.find(arg => arg.startsWith('--hours='));
const graceFlag = argv.find(arg => arg.startsWith('--grace-minutes='));
const hoursToCheck = Math.max(1, Number(hoursFlag ? hoursFlag.split('=')[1] : 6) || 6);
const graceMinutes = Math.max(0, Number(graceFlag ? graceFlag.split('=')[1] : 20) || 20);
const now = new Date();
const currentSlotDate = new Date(now);
currentSlotDate.setMinutes(0, 0, 0);

const expectedSlots = [];
for (let i = hoursToCheck - 1; i >= 0; i -= 1) {
  expectedSlots.push(slotFor(new Date(currentSlotDate.getTime() - i * 60 * 60 * 1000)));
}

const logText = readText(logPath);
const logLines = logText.split(/\r?\n/).filter(Boolean);
const hourlySeen = new Set();
const dailySeen = new Set();
for (const line of logLines) {
  const hourlyMatch = line.match(/\[(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) CEST\] hourly update/);
  if (hourlyMatch) hourlySeen.add(`${hourlyMatch[1]} ${hourlyMatch[2]}:00`);
  const dailyMatch = line.match(/\[(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) CEST\] daily ticket reminder/);
  if (dailyMatch) dailySeen.add(dailyMatch[1]);
}

const currentVienna = nowVienna(now);
const currentMinutesIntoHour = Number(currentVienna.minute || '0');
const effectiveExpectedSlots = currentMinutesIntoHour < graceMinutes ? expectedSlots.slice(0, -1) : expectedSlots;
const missingHourlySlots = effectiveExpectedSlots.filter(slot => !hourlySeen.has(slot));
const state = readJson(statePath, null);
const report = {
  generated_at: nowVienna().stamp,
  audit_window_hours: hoursToCheck,
  grace_minutes: graceMinutes,
  expected_hourly_slots: expectedSlots,
  effective_expected_hourly_slots: effectiveExpectedSlots,
  missing_hourly_slots: missingHourlySlots,
  last_daily_slot_seen_in_log: Array.from(dailySeen).sort().slice(-1)[0] || null,
  state_snapshot: state,
  status: missingHourlySlots.length === 0 ? 'pass' : 'fail',
  next_expected_hourly_slot: slotFor(new Date(currentSlotDate.getTime() + 60 * 60 * 1000)),
};

ensureDir(reportPath);
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
process.stdout.write(JSON.stringify(report, null, 2) + '\n');
