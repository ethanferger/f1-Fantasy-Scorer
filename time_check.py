#today = datetime.now()
# today > datetime(2026, 3, 8, 2, 0)
# #print(today)

# current_round = 4
# schedule = fastf1.get_event_schedule(2026)
# event = schedule.get_event_by_round(current_round)
# event

# current_round_datetime_utc = event[f"Session{current_round}DateUtc"]#.date()
# #current_round_datetime_central = current_round_datetime_utc - timedelta(hours = 5)
# #current_round_datetime_central

# def check_daylight_savings():
#     if today > datetime(2026, 3, 8, 2, 0) and today < datetime(2026, 11, 1, 2, 0):
#         print("This is the spring forward time and is utc - 5 hours")
#         current_round_datetime_central_buffer = current_round_datetime_utc - timedelta(hours = 5)
#     else:
#         print("this is the fall back time and is utc -6 hours")
#         current_round_datetime_central_buffer = current_round_datetime_utc - timedelta(hours = 6)
    



# for i in range(1,6):
#     print(event[f"Session{i}"], event[f"Session{i}DateUtc"])
