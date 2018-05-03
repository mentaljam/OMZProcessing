#### Functions and commands

# Recursive file search function
rwildcard=$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2) $(filter $(subst *,%,$2),$d))

# Platform commands
ifeq ($(OS),Windows_NT)
    python3 = $(addprefix "$(OSGEO4W_ROOT)",/bin/python3)
    pylupdate5 = cmd //c $(python3) -m PyQt5.pylupdate_main
else
    pylupdate5 = pylupdate5
endif


#### Configuration

# Plugin name
PLUGINNAME   = omzprocessing

# Locales
LOCALES      = ru

# List ts and qm files
TS_FILES     = $(patsubst %,i18n/omzprocessing_%.ts,$(LOCALES))
QM_FILES     = $(patsubst %.ts,%.qm,$(TS_FILES))

# List py files
PY_FILES     = $(call rwildcard,,*.py)

# List images
PNG_FILES	 = $(call rwildcard,,*.png)

# Install files
INSTALL_FILES = \
	$(PY_FILES) \
    $(QM_FILES) \
    $(PNG_FILES) \
    metadata.txt


#### Targets

default: qm

.PHONY : help
help:
	@echo
	@echo "------------------------------"
	@echo "        Build targets"
	@echo "------------------------------"
	@echo qm
	@echo update_ts
	@echo update_ts_clean
	@echo package
	@echo clean

$(QM_FILES): %.qm : %.ts
	@echo "qm:  $@"
	@lrelease -silent $<

qm: $(QM_FILES)

$(TS_FILES):
	@echo "ts:  $@"
	@$(pylupdate5) $(PY_FILES) -ts $@

update_ts:
	@echo
	@echo "------------------------------"
	@echo "    Updating translations"
	@echo "------------------------------"
	@$(foreach var,$(LOCALES),echo $(var); $(pylupdate5) $(PY_FILES) -ts $(TS_FILES);)
	@echo done!

update_ts_clean:
	@echo
	@echo "------------------------------"
	@echo "Removing obsolete translations"
	@echo "------------------------------"
	@$(foreach var,$(LOCALES),echo $(var); $(pylupdate5) $(PY_FILES) -ts $(TS_FILES) -noobsolete;)
	@echo done!

package: $(INSTALL_FILES)
	@echo
	@echo "------------------------------"
	@echo "      Preparing package"
	@echo "------------------------------"
	@mkdir -p dist
	@rm -fv $(wildcard dist/$(PLUGINNAME)*.zip)
	@$(eval ARCHIVE := $(PLUGINNAME)_$(strip $(shell awk -F = '/version/ {print $$2}' metadata.txt)).zip)
	@echo Adding files to $(ARCHIVE):
	@$(eval INSTALL_WITH_PREFIX := $(foreach file,$(INSTALL_FILES), $(PLUGINNAME)/$(file)))
	@cd ..; zip $(PLUGINNAME)/dist/$(ARCHIVE) $(INSTALL_WITH_PREFIX)
	@echo done!

.PHONY : clean
clean:
	@echo
	@echo "------------------------------"
	@echo "           Cleaning"
	@echo "------------------------------"
	@rm -fv $(QM_FILES)
	@rm -fvr dist
	@echo done!
