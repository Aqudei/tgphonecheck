from phonechecker import tasks

def new_csv_uploaded(instance, created):
    # csv_file = get_csv_file
    # create phone numbers
    if created:
        tasks.csv_import.delay(instance.batch_id)
        tasks.run_telethon.delay(instance.batch_id)