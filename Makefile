
CODE_DIR := src

.PHONY: all
all:
	@$(MAKE) -C $(CODE_DIR)

.PHONY: test
test:
	@$(MAKE) -C $(CODE_DIR) test

.PHONY: clean
clean:
	@$(MAKE) -C $(CODE_DIR) clean

