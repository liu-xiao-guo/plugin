# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-

import logging
import os
import glob
from pprint import pprint

import snapcraft

logger = logging.getLogger(__name__)

def _dump(name, obj):
    for attr in dir(obj):
        # logger.warning("obj.%s = %s", attr, getattr(obj, attr))
        func = getattr(obj, attr, None)
        if func:
            logger.warning("%s.%s = %s",name, attr, func)
            
    logger.warning("===================================")

class MyPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['myprop'] = {
            'type': 'string',
            'default': ''
        }

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['build-properties'].append('myprop')

        return schema
        
    def _copy(self, path_copyto):
        path = os.path.join(path_copyto, "meta/hooks/")
        logger.warning("path: %s", path);
        os.makedirs(os.path.dirname(path), exist_ok=True)
        source = self.builddir + "/" + self.options.myprop
        logger.warning("source: %s", source)
        destination = path + self.options.myprop
        logger.warning("destination: %s", destination)
        snapcraft.common.link_or_copy(source, destination, False)
                
    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        logger.warning("__init__ begins name: %s", name)
        logger.warning("options.source: %s", options.source)
        logger.warning("options.myprop: %s", options.myprop) 
        logger.warning("self.builddir: %s", self.builddir)
        logger.warning("self.installdir: %s", self.installdir)
        # logger.warning("self.project.parallel_build_count: %d", self.project.parallel_build_count)
        # logger.warning("self.project.arch_triplet: %s", self.project.arch_triplet)
        # logger.warning("self.project.stage_dir: %s", self.project.stage_dir)
       
        logger.warning("Going to add the needed build packages...")
        # self.build_packages.append('golang-go')
        _dump("options", options)
        _dump("project", project)
        
        logger.warning("build-packages:")
        for pkg in options.build_packages:
            logger.warning("build package: %s", pkg)

    def build(self):
        # setup build directory
        super().build()
        logger.warning("build begins ... ")
        
        # creating a dir under /parts/<part>/build/setup/gui
        self._copy(self.builddir)
        
        # we need to do the same for the installation dir
        self._copy(self.installdir)
       
    def pull(self):
        super().pull()
        logger.warning("pull begins ... ")                
       
    def clean_pull(self):
        super().clean_pull()       
        logger.warning("clean pull begins ... ")
      

