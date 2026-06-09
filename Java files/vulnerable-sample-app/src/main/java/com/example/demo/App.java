package com.example.demo;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;
import com.google.common.base.Joiner;

import java.util.Arrays;
import java.util.Map;

/**
 * Sample application exercising several outdated/vulnerable dependencies.
 * Used to test the dependency remediation agent.
 */
public class App {

    private static final Logger LOGGER = LogManager.getLogger(App.class);

    public static void main(String[] args) throws Exception {
        App app = new App();

        // log4j 2.14.1 (Log4Shell)
        LOGGER.info("Starting vulnerable-sample-app");

        // jackson-databind 2.9.8
        String json = app.toJson();
        LOGGER.info("Serialized JSON: {}", json);

        // snakeyaml 1.30
        Map<String, Object> config = app.loadYaml();
        LOGGER.info("Loaded YAML keys: {}", config.keySet());

        // guava 24.1.1
        String joined = Joiner.on(", ").join(Arrays.asList("a", "b", "c"));
        LOGGER.info("Guava joined: {}", joined);
    }

    public String toJson() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.writeValueAsString(Map.of("app", "demo", "version", 1));
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> loadYaml() {
        Yaml yaml = new Yaml();
        return yaml.load("app: demo\nversion: 1\nenabled: true\n");
    }
}
