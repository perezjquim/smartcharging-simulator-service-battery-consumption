from nameko.events import EventDispatcher
from nameko.rpc import rpc

from model.exceptions import NotFound

import json

import tensorflow as tf

class ModelService:

    BATTERY_CONSUMPTION_PER_KM_AVG = 0.504
    BATTERY_CONSUMPTION_PER_KM_STDDEV = 0.676

    name = 'model_battery_consumption'

    event_dispatcher = EventDispatcher()

    @rpc
    def get_final_battery_level(self, initial_battery_level, travel_distance):
        battery_consumption_per_km = self.generate_battery_consumption_per_km()
        final_battery_level = initial_battery_level - ( travel_distance * battery_consumption_per_km )

        response = json.dumps({'final_battery_level': final_battery_level})
        return response

    def generate_battery_consumption_per_km(self):
        shape = [1,1]
        min_battery_consumption_per_km = self.BATTERY_CONSUMPTION_PER_KM_AVG - self.BATTERY_CONSUMPTION_PER_KM_STDDEV
        max_battery_consumption_per_km = self.BATTERY_CONSUMPTION_PER_KM_AVG + self.BATTERY_CONSUMPTION_PER_KM_STDDEV

        tf_random = tf.random.uniform(
                shape=shape,
                minval=min_battery_consumption_per_km,
                maxval=max_battery_consumption_per_km,
                dtype=tf.dtypes.float32,
                seed=None,
                name=None
        )
        tf_var = tf.Variable( tf_random )

        tf_init = tf.initialize_all_variables()
        tf_session = tf.Session()
        tf_session.run(tf_init)

        tf_return = tf_session.run(tf_var)
        battery_consumption_per_km = float( tf_return[ 0 ][ 0 ] )

        return battery_consumption_per_km
