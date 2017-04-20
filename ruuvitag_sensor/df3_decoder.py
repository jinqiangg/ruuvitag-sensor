from ruuvitag_sensor.log import logger


class Df3Decoder(object):
    '''
    Decodes data from RuuviTag with Data Format 3
    Protocol specification:
    https://github.com/ruuvi/sensor-protocol-for-eddystone-url
    '''

    def _get_temperature(self, data):
        '''Return temperature in celsius'''
        temp = (data[1] << 1 >> 1) + (data[2] / 100)
        sign = (data[1] >> 7)
        if sign == 0:
            return round(temp, 2)
        return round(-1 * temp, 2)

    def _get_humidity(self, data):
        '''Return humidity %'''
        return data[0] * 0.5

    def _get_pressure(self, data):
        '''Return air pressure hPa'''
        pres = (data[3] << 8) + data[4] + 50000
        return pres / 100

    def _get_acceleration(self, data):
        '''Return air pressure hPa'''
        acc_x = ((data[6] << 8) + data[7])
        acc_y = ((data[8] << 8) + data[9])
        acc_z = ((data[10] << 8) + data[11])
        return (acc_x, acc_y, acc_z)

    def _get_battery(self, data):
        '''Return air pressure hPa'''
        battery = ((data[12] << 8) + data[13])
        return battery

    def decode_data(self, data):
        '''
        Decode sensor data.

        Returns:
            Sensor values in dictionary
        '''
        try:
            byte_data = bytes.fromhex(data)
            return {
                'humidity': self._get_humidity(byte_data),
                'temperature': self._get_temperature(byte_data),
                'pressure': self._get_pressure(byte_data),
                'acceleration': self._get_acceleration(byte_data),
                'battery': self._get_battery(byte_data)
            }
        except:
            logger.exception('Value: %s not valid', data)
            return None