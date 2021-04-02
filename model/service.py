from nameko.events import EventDispatcher
from nameko.rpc import rpc

from model.exceptions import NotFound

import json

import tensorflow as tf

class ModelService:

    BATTERY_CONSUMPTION_PER_KM_AVG = 0.504
    BATTERY_CONSUMPTION_PER_KM_STDDEV = 0.676

    name = 'model_energysim_travel_final_battery_level'

    event_dispatcher = EventDispatcher( )

    @rpc
    def get_final_battery_level( self, initial_battery_level, travel_distance ):
        travel_battery_consumption = self.generate_battery_consumption( )
        final_battery_level = int( initial_battery_level ) - ( float( travel_distance ) * travel_battery_consumption )

        response = json.dumps( { 'final_battery_level': final_battery_level } )
        return response

    def generate_battery_consumption(self):
        shape = [ 1,1 ]
        min_battery_consumption = ModelService.BATTERY_CONSUMPTION_PER_KM_AVG - ModelService.BATTERY_CONSUMPTION_PER_KM_STDDEV
        max_battery_consumption = ModelService.BATTERY_CONSUMPTION_PER_KM_AVG + ModelService.BATTERY_CONSUMPTION_PER_KM_STDDEV

        tf_random = tf.random_uniform(
                shape=shape,
                minval=min_battery_consumption,
                maxval=max_battery_consumption,
                dtype=tf.float32,
                seed=None,
                name=None
        )
        tf_var = tf.Variable( tf_random )

        tf_init = tf.global_variables_initializer( )
        tf_session = tf.Session( )
        tf_session.run( tf_init )

        tf_return = tf_session.run( tf_var )
        travel_final_battery_level = float( tf_return[ 0 ][ 0 ] )

        return travel_final_battery_level
