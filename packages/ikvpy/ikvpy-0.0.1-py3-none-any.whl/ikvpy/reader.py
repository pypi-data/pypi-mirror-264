from typing import Optional
from client import IKVReader
from clientoptions import ClientOptions
from writer import IKVWriterImpl
from bin_manager import NativeBinaryManager
from utils import is_valid_str_or_raise

import native_reader
import schemas.common_pb2 as common_pb2

class IKVReaderImpl(IKVReader):
    def __init__(self, client_options: ClientOptions):
        if client_options is None:
            raise TypeError("client_options are required and can't be None")
        self.client_options = client_options
        self.native_reader = None # initialized at startup

    def startup(self):
        # download dll and initialize native reader
        mount_dir = is_valid_str_or_raise(self.client_options.get_ikv_config().stringConfigs["mount_directory"])
        bin_manager = NativeBinaryManager(mount_dir=mount_dir)

        dll_path = bin_manager.get_path_to_dll()
        if dll_path is None:
            raise RuntimeError("Cannot download IKV native binary")
        self.native_reader = native_reader.NativeReader(dll_path)

        # fetch server supplied config and merge with client cfg
        writer: IKVWriterImpl = IKVWriterImpl(self.client_options)
        writer.startup()
        server_cfg = writer.fetch_server_supplied_config()
        writer.shutdown()
        if not isinstance(server_cfg, common_pb2.IKVStoreConfig):
            raise RuntimeError("cannot fetch startup cfg from IKV cloud for given client options")
        merged_cfg = self._merge_configs(server_cfg)
        ikv_config_bytes = bytes(merged_cfg.SerializeToString())
        
        self.native_reader.open(ikv_config_bytes)

    def shutdown(self):
        self.native_reader.close()

    # nullable return type
    def get_bytes_value(self, primary_key, field_name: str) -> Optional[bytes]:
        if isinstance(primary_key, str):
            return self.native_reader.get_field_value(bytes(primary_key.encode('utf-8')), field_name)
        
        if isinstance(primary_key, bytes):
            return self.native_reader.get_field_value(primary_key, field_name)
        
        if isinstance(primary_key, bytearray):
            return self.native_reader.get_field_value(bytes(primary_key), field_name)
        
        raise TypeError("unsupported primary_key type: {}, supported: str/bytes/bytearray".format(type(primary_key)))

    def get_string_value(self, primary_key, field_name: str) -> Optional[str]:
        maybe_value = self.get_bytes_value(primary_key, field_name)
        
        if maybe_value is None:
            return None
        
        return maybe_value.decode('utf-8')
    
    def _merge_configs(self, server_cfg: common_pb2.IKVStoreConfig) -> common_pb2.IKVStoreConfig:
        client_cfg = self.client_options.get_ikv_config()

        string_configs = server_cfg.stringConfigs if server_cfg.stringConfigs is not None else {}
        if client_cfg.stringConfigs is not None:
            for k,v in client_cfg.stringConfigs.items():
                string_configs[k] = v

        intConfigs = server_cfg.intConfigs if server_cfg.intConfigs is not None else {}
        if client_cfg.intConfigs is not None:
            for k,v in client_cfg.intConfigs.items():
                intConfigs[k] = v

        floatConfigs = server_cfg.floatConfigs if server_cfg.floatConfigs is not None else {}
        if client_cfg.floatConfigs is not None:
            for k,v in client_cfg.floatConfigs.items():
                floatConfigs[k] = v

        bytesConfigs = server_cfg.bytesConfigs if server_cfg.bytesConfigs is not None else {}
        if client_cfg.bytesConfigs is not None:
            for k,v in client_cfg.bytesConfigs.items():
                bytesConfigs[k] = v

        booleanConfigs = server_cfg.booleanConfigs if server_cfg.booleanConfigs is not None else {}
        if client_cfg.booleanConfigs is not None:
            for k,v in client_cfg.booleanConfigs.items():
                booleanConfigs[k] = v

        return common_pb2.IKVStoreConfig(stringConfigs=string_configs, intConfigs=intConfigs,\
                floatConfigs=floatConfigs, bytesConfigs=bytesConfigs, booleanConfigs=booleanConfigs)