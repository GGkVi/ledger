#!/bin/bash
set -eo pipefail

# Colors
COLOR_GREEN=$(tput setaf 2)
COLOR_BLUE=$(tput setaf 4)
COLOR_NC=$(tput sgr0) # No Color

echo ""
echo "${COLOR_BLUE}============================"
echo "  Code Formatter Started"
echo "============================${COLOR_NC}"
echo ""

# 1) isort

echo "${COLOR_BLUE}Running isort...${COLOR_NC}"
poetry run isort .
echo "${COLOR_GREEN}isort OK${COLOR_NC}"
echo ""


# 2) ruff (정리 + 포맷)
echo "${COLOR_BLUE}Running ruff (lint + fix)...${COLOR_NC}"
poetry run ruff check --select I --fix
poetry run ruff check --fix
echo "${COLOR_GREEN}ruff OK${COLOR_NC}"
echo ""

# 3) black
echo "${COLOR_BLUE}Running black...${COLOR_NC}"
poetry run black .
echo "${COLOR_GREEN}black OK${COLOR_NC}"
echo ""

echo "${COLOR_GREEN}✨ Code formatting completed successfully! ✨${COLOR_NC}"
