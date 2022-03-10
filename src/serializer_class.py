import sys

import pickle,lzma,base64,io

class Serializer:
    #override the python serializer
    class Find(pickle.Unpickler):
        def find_class(self,name,global_name):
            return super().find_class(name,global_name)

    def serializer(self):
        compressor = lzma.LZMACompressor()
        to_serializ = pickle.dumps(self, fix_imports=True)
        compressed = compressor.compress(to_serializ)
        compressed += compressor.flush()
        decoded = base64.b85encode(compressed).decode("ascii")
        return decoded

    @staticmethod
    def deserializer(to_deserializ):
        decompressor = lzma.LZMADecompressor()
        decoded = base64.b85decode(to_deserializ)
        decompressed = decompressor.decompress(decoded)
        pickled = Serializer.Find(io.BytesIO(decompressed))
        h=pickled.load()
        return h
