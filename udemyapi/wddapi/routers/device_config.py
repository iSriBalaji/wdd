#this endpoint contains all the config of a device
# this endpoint will be updated every week in an automated way from the device
# if the device_id did not exist in the table create it or update the record if therer are any changes
# have a hash_id along with the table schema
# these fields are updated infrequently


# IN the same file have the endpoints for the device config dynamic
# this table has fields that are frequently updated
# run automatically every 3 hours