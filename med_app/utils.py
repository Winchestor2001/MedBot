from datetime import datetime, timedelta


def check_dates(user_data, doctor_data):
    user_dates = [item.confirance_date for item in user_data]
    doctor_dates = [item.work_time for item in doctor_data.date_set.all()]

    all_dates = user_dates + doctor_dates

    sorted_dates = sorted(all_dates)

    filtered_doctor_dates = []

    for doctor_date in sorted_dates:
        is_conflict = any(abs(doctor_date - user_date) < timedelta(minutes=30) for user_date in user_dates)
        if not is_conflict and doctor_date in doctor_dates:
            filtered_doctor_dates.append(doctor_date)

    print(filtered_doctor_dates)
    return filtered_doctor_dates
